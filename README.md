# BookBrain-Azure 

An advanced serverless platform that revolutionizes educational content processing and study analytics.

## Key Features

<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20bookBrain%20features.png" width="100%">

## Tech Stack

- Azure Functions
- Python
- Azure Storage
- PostgreSQL
- OpenAI Integration
- Swagger API Documentation

## Components

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

## Setup & Configuration

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

## Environment Variables

Required environment variables (see `.env.example`):
- `AZURE_STORAGE_CONNECTION_STRING`: Azure Storage connection string
- `DB_HOST`: Database host
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- Other API endpoints and configuration values

## Target Users

- Educational Institutions
- E-Learning Platforms
- Students and Educators
- Content Publishers
- Learning Management Systems

## API Documentation

API documentation is available via Swagger UI at `/api/swagger/ui`.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with  for the future of education