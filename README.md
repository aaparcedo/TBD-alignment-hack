<p align="center">
  <img src="logo.png" alt="Project Logo" width="200"/>
</p>

<h1 align="center">Are You Sure About That?</h1>

<p align="center">
  <strong>A Chain-of-Thought Faithfulness Detection Game</strong>
</p>

<p align="center">
  <a href="#demo">View Demo</a> •
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#installation">Installation</a> •
  <a href="#deployment">Deployment</a>
</p>

## 🎯 About

"Are You Sure About That?" is an interactive web application that challenges users to evaluate the faithfulness of AI model responses to subjective questions. The game presents users with two different model explanations and asks them to identify which demonstrates unfaithful Chain-of-Thought reasoning.

## ✨ Features

- Interactive question-answer interface with multiple-choice selection
- Real-time evaluation using Claude API
- Side-by-side comparison of model responses
- Automated scoring and feedback system
- Comprehensive summary of user performance
- User feedback collection for response quality
- Progress tracking across questions

## 🛠️ Tech Stack

- **Frontend & API**: Streamlit
- **AI Model**: Claude 3.5 Sonnet (Anthropic)
- **Server**: DigitalOcean Droplet
- **Reverse Proxy**: Nginx
- **Domain & Security**: Cloudflare
- **Containerization**: Docker
- **Version Control**: Git

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/are-you-sure-about-that.git
cd are-you-sure-about-that
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

5. Run the application:
```bash
streamlit run app.py
```

## 🌐 Deployment

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t streamlit-claude .
```

2. Run the container:
```bash
docker run -d \
  --name streamlit-app \
  --restart unless-stopped \
  -p 8501:8501 \
  --env-file .env \
  streamlit-claude
```

### Server Setup

1. Configure Nginx:
```bash
sudo vim /etc/nginx/sites-available/streamlit
```

2. Add the following configuration:
```nginx
server {
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

3. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Domain Setup

1. Configure DNS records in Cloudflare:
   - Add A record pointing to your DigitalOcean Droplet IP
   - Add www CNAME record pointing to your domain
   - Enable SSL/TLS protection

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
