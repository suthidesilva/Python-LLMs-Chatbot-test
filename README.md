# Physics Helper Tool

Welcome to the Physics Helper Tool repository! This tool is designed to assist users in solving physics problems and finding relevant sources for their queries. Whether you're a student studying physics or an enthusiast exploring the subject, this tool aims to make your learning journey easier.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Physics Helper Tool is a Python-based application that integrates various APIs and AI models to provide assistance with physics-related tasks. It leverages the power of language models like OpenAI's GPT-3, as well as external services such as Google Scholar and Wolfram Alpha, to deliver accurate solutions and relevant sources.

## Features

- **Question Classification:** Automatically categorizes user queries into two types: 'sources' or 'solve', based on the nature of the question.
- **Source Retrieval:** Searches Google Scholar for articles, books, and other sources related to the user's query, providing valuable references for further study.
- **Problem Solving:** Utilizes Wolfram Alpha API to solve computational physics problems and provides theoretical solutions for theoretical physics questions.
- **Integration with OpenAI's GPT-3:** Employs GPT-3 for natural language understanding and response generation, enhancing the tool's ability to interact with users effectively.

## Installation

To install and run the Physics Helper Tool locally, follow these steps:

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/your-username/physics-helper-tool.git
   ```

2. Navigate to the project directory:
   ```
   cd physics-helper-tool
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your API keys for Wolfram Alpha, Google Scholar (SERP), and OpenAI's GPT-3 by setting environment variables in a `.env` file.

5. Run the main Python script:
   ```
   python main.py
   ```

## Usage

Once the tool is set up and running, you can interact with it by providing physics-related questions or queries. The tool will classify your question, retrieve relevant sources if needed, and provide solutions or references accordingly.

Here's an example of how to use the tool:

```python
question = "What is the speed of an object falling from a height of 100 meters?"
help_with_physics(question)
```

## Contributing

Contributions to the Physics Helper Tool are welcome! If you have ideas for new features, improvements, or bug fixes, please feel free to open an issue or submit a pull request. 

Before contributing, please review the [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
