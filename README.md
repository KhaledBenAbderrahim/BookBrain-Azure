# <div align="center">🧠 BookBrain-Azure</div>

<div align="center">
  <p>
    <strong>An advanced serverless platform that revolutionizes educational content processing and study analytics.</strong>
  </p>
  <p>
    <a href="#key-features">Features</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#components">Components</a> •
    <a href="#setup--configuration">Setup</a> •
    <a href="#api-documentation">API Docs</a>
  </p>
</div>

<div align="center">
  <img src="https://img.shields.io/badge/Azure%20Functions-0062AD?style=for-the-badge&logo=azure-functions&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
</div>

---

## 🎯 Key Features

<div align="center">
  <img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20bookBrain%20features.png" width="80%">
</div>

## 🛠️ Tech Stack

<div style="background-color: #f6f8fa; padding: 20px; border-radius: 8px;">
<table>
<tr>
<td align="center" width="25%">
<img width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/azure/azure-original.svg">
<br>Azure Functions
</td>
<td align="center" width="25%">
<img width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">
<br>Python
</td>
<td align="center" width="25%">
<img width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg">
<br>PostgreSQL
</td>
<td align="center" width="25%">
<img width="40" src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/openai.svg">
<br>OpenAI
</td>
</tr>
</table>
</div>

## 💡 Components

<table>
<tr>
<td width="50%">

### 1. PDF Chunking Function
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20pdf%20chunking%20function.png" width="100%">

</td>
<td width="50%">

### 2. Study Progress Function
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20Study%20progress%20function.png" width="100%">

</td>
</tr>
<tr>
<td width="50%">

### 3. Upload Book Function
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20upload%20book%20function.png" width="100%">

</td>
<td width="50%">

### 4. Hourly Study Digest
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20Hourly%20Study%20Digest.png" width="100%">

</td>
</tr>
</table>

## ⚙️ Setup & Configuration

<details>
<summary>📥 Installation Steps</summary>

1. Clone the repository
```bash
git clone https://github.com/KhaledBenAbderrahim/BookBrain-Azure.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment variables
   - Copy `.env.example` to `.env`
   - Fill in your Azure credentials and other settings

4. Start the Azure Functions host
```bash
func start
```
</details>

<details>
<summary>🔑 Environment Variables</summary>

Required environment variables (see `.env.example`):
- `AZURE_STORAGE_CONNECTION_STRING`: Azure Storage connection string
- `DB_HOST`: Database host
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- Other API endpoints and configuration values
</details>

## 👥 Target Users

<div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
  <div style="text-align: center; padding: 10px;">
    <h3>🎓</h3>
    Educational Institutions
  </div>
  <div style="text-align: center; padding: 10px;">
    <h3>💻</h3>
    E-Learning Platforms
  </div>
  <div style="text-align: center; padding: 10px;">
    <h3>📚</h3>
    Students and Educators
  </div>
  <div style="text-align: center; padding: 10px;">
    <h3>📖</h3>
    Content Publishers
  </div>
</div>

## 📚 API Documentation

API documentation is available via Swagger UI at `/api/swagger/ui`.

## 🤝 Contributing

<details>
<summary>How to Contribute</summary>

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
</details>

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  Built with ❤️ for the future of education
</div>