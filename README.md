# <div align="center">BookBrain-Azure</div>

<div align="center">
  <img src="https://img.shields.io/badge/azure%20functions-%230062CC.svg?style=for-the-badge&logo=azure-functions&logoColor=white">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/OpenAI-%23412991.svg?style=for-the-badge&logo=openai&logoColor=white">
</div>

<div align="center">
  <p><i>An advanced serverless platform that revolutionizes educational content processing and study analytics.</i></p>
  <p>
    <b>Developed by <a href="https://github.com/KhaledBenAbderrahim">Khaled Ben Abderrahim</a></b>
  </p>
</div>

<br>

<div align="center">

## 🚀 Key Features
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20bookBrain%20features.png" width="80%">
</div>

<br>

<div align="center">

## 💻 Tech Stack
<table align="center">
<tr>
<td align="center">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/azure/azure-original.svg" width="40" height="40"/>
<br>Azure Functions
</td>
<td align="center">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="40" height="40"/>
<br>Python
</td>
<td align="center">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" width="40" height="40"/>
<br>PostgreSQL
</td>
<td align="center">
<img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/openai.svg" width="40" height="40"/>
<br>OpenAI
</td>
</tr>
</table>
</div>

<br>

## 🔧 Components

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

<br>

## ⚙️ Setup & Configuration

<details>
<summary>📝 Installation Steps</summary>

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

<br>

## 🎯 Target Users

<table align="center">
<tr>
<td align="center">📚 Educational Institutions</td>
<td align="center">💻 E-Learning Platforms</td>
<td align="center">👨‍🎓 Students and Educators</td>
</tr>
<tr>
<td align="center">📖 Content Publishers</td>
<td align="center">🏫 Learning Management Systems</td>
<td align="center">📱 Educational Apps</td>
</tr>
</table>

<br>

## 📚 API Documentation

API documentation is available via Swagger UI at `/api/swagger/ui`.

## Contributing

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

<div align="center">
<br>

---

Built with ❤️ by [Khaled Ben Abderrahim](https://github.com/KhaledBenAbderrahim)
</div>