module.exports = {
  apps: [
    {
      name: 'iost-bot',
      script: 'bot.py',
      interpreter: 'python3',
      cwd: '.',
      env: {
        NODE_ENV: 'production'
      },
      error_file: './logs/bot-error.log',
      out_file: './logs/bot-out.log',
      log_file: './logs/bot-combined.log',
      time: true,
      restart_delay: 5000,
      max_restarts: 10,
      autorestart: true
    },
    {
      name: 'iost-tracker',
      script: 'tracker_server.py',
      interpreter: 'python3',
      cwd: '.',
      env: {
        NODE_ENV: 'production',
        PORT: 5000
      },
      error_file: './logs/tracker-error.log',
      out_file: './logs/tracker-out.log',
      log_file: './logs/tracker-combined.log',
      time: true,
      restart_delay: 5000,
      max_restarts: 10,
      autorestart: true
    }
  ]
};