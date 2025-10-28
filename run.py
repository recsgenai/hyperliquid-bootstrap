from bot.runner import Runner

def main():
    runner = Runner(config_path="config.yaml")
    runner.run_simulation(steps=200)

if __name__ == '__main__':
    main()
