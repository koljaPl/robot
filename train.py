"""Simple reproducible PPO training; headless physics needs no display."""
import argparse
import json
from pathlib import Path
import hashlib
import torch
from dataclasses import asdict
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback, CallbackList
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from humanoid_env import HumanoidEnv
from robot_config import ROOT, DR


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--steps", type=int, default=1_000_000)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--randomize", action="store_true")
    p.add_argument("--output", type=Path, default=ROOT / "runs" / "ppo")
    p.add_argument("--episode-seconds", type=float, default=30)
    p.add_argument("--resume", type=Path)
    args = p.parse_args()
    torch.set_num_threads(1)
    if args.steps <= 0:
        p.error("--steps must be positive")
    args.output.mkdir(parents=True, exist_ok=True)
    env = HumanoidEnv(domain_randomization=args.randomize, episode_seconds=args.episode_seconds)
    check_env(env, warn=True)
    train_env = Monitor(env, str(args.output / "training"))
    evaluation = Monitor(HumanoidEnv(domain_randomization=False, episode_seconds=args.episode_seconds))
    evaluation.reset(seed=args.seed + 10_000)
    manifest = {"seed": args.seed, "steps": args.steps, "randomization": args.randomize,
                "randomization_config": asdict(DR), "episode_seconds": args.episode_seconds,
                "xml_sha256": hashlib.sha256((ROOT / "robot.xml").read_bytes()).hexdigest(),
                "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                  for name in ("robot_config.py", "humanoid_env.py", "servo_control.py", "imu_observation.py", "physical_spec.json")},
                "status": "simulation training; does not establish hardware walking"}
    (args.output / "training_config.json").write_text(json.dumps(manifest, indent=2) + "\n")
    callbacks = CallbackList([
        CheckpointCallback(save_freq=10_000, save_path=str(args.output / "checkpoints"), name_prefix="ppo"),
        EvalCallback(evaluation, best_model_save_path=str(args.output / "best"), log_path=str(args.output / "eval"),
                     eval_freq=10_000, n_eval_episodes=5, deterministic=True)])
    if args.resume:
        model = PPO.load(args.resume, env=train_env, device="cpu")
        model.set_random_seed(args.seed)
        model.tensorboard_log = str(args.output / "tensorboard")
    else:
        model = PPO("MlpPolicy", train_env, learning_rate=3e-4, n_steps=1024, batch_size=64,
                    n_epochs=10, gamma=0.99, gae_lambda=0.95, clip_range=0.2,
                    ent_coef=0.005, policy_kwargs={"net_arch": [64, 64]},
                    tensorboard_log=str(args.output / "tensorboard"), seed=args.seed,
                    device="cpu", verbose=1)
    try:
        model.learn(total_timesteps=args.steps, callback=callbacks, reset_num_timesteps=not bool(args.resume))
        model.save(args.output / "final_model")
    finally:
        train_env.close()
        evaluation.close()


if __name__ == "__main__":
    main()
