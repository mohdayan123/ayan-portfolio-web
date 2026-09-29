"""
Flask Application for Mohd Ayan Portfolio & DevOps Showcase
Author: Mohd Ayan (B.Tech CSE IBM, TMU Moradabad)
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static')

# In-memory storage for contact inquiries (can be piped to AWS RDS or DynamoDB)
MESSAGES_LOG = []

@app.route('/')
def home():
    """Renders the single-file Three.js 3D portfolio."""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    DevOps Healthcheck endpoint for AWS ALB / Target Groups / Docker HEALTHCHECK
    """
    return jsonify({
        "status": "healthy",
        "service": "mohd-ayan-devops-portfolio",
        "timestamp": datetime.utcnow().isoformat(),
        "runtime": "Python/Flask",
        "uptime": "100%",
        "version": "1.0.0"
    }), 200

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """
    Endpoint for portfolio contact messages
    """
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        name = data.get('name') or data.get('senderName')
        email = data.get('email') or data.get('senderEmail')
        message = data.get('message') or data.get('senderMessage')

        if not name or not email or not message:
            return jsonify({
                "success": False,
                "error": "Please provide your name, email, and message."
            }), 400

        entry = {
            "name": name,
            "email": email,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        MESSAGES_LOG.append(entry)

        # Output to console log for Docker/Jenkins container visibility
        print(f"[CONTACT INQUIRY] From: {name} <{email}> at {entry['timestamp']}")
        print(f"Message content: {message}\n")

        return jsonify({
            "success": True,
            "message": f"Thank you, {name}! Your message has been received by Mohd Ayan.",
            "reference_id": f"INQ-{len(MESSAGES_LOG):04d}",
            "received_at": entry['timestamp']
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/metrics', methods=['GET'])
def metrics():
    """
    Simple Prometheus / monitoring metrics endpoint
    """
    return jsonify({
        "inquiries_received": len(MESSAGES_LOG),
        "active_containers": 1,
        "environment": os.environ.get("FLASK_ENV", "production")
    }), 200

if __name__ == '__main__':
    # Listen on port specified by environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    print(f"Starting Flask server on http://0.0.0.0:{port}...")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
