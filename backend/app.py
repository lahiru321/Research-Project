# from flask import Flask
# import subprocess

# app = Flask(__name__)
# process = None

# @app.route('/start', methods=['POST'])
# def start_detection():
#     global process
#     if not process:
#         process = subprocess.Popen(['python', 'services/engagement_system.py'])
#     return 'Engagement detection started', 200

# @app.route('/end', methods=['POST'])
# def end_detection():
#     global process
#     if process:
#         process.terminate()
#         process = None
#     return 'Engagement detection ended', 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
