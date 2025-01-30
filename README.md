# Rasa Chat Bot for Custom Actions

## Overview
The Rasa Chat Bot is a conversational agent designed to address user queries and execute custom actions. It utilizes the Rasa framework, employing the DIET Classifier for intent and entity recognition. Duckling is integrated for extracting additional entities like Email and Duration. The chatbot is hosted on Contabo using Docker and Docker Compose, trained and fine-tuned to handle specific site requirements, making it an ideal solution for businesses and developers seeking automated, customizable interactions.

### Intended Audience:
- Developers
- Businesses
- Organizations seeking customizable and extensible solutions for automated interactions and custom actions

---

## Libraries and Frameworks

This project utilizes the following libraries and frameworks:

- **Rasa**: The core framework for building the chatbot and managing conversational flows.
- **DIET Classifier**: Used for intent and entity recognition within user queries.
- **Duckling**: A tool for extracting additional entities such as Email and Duration from text.
- **Docker & Docker Compose**: Used for containerization and deployment of the Rasa chatbot.
- **Contabo**: Hosting provider used for deploying the Dockerized chatbot.
- **torch**: The PyTorch framework, essential for certain components of the Rasa framework.

---

## Contributing

We welcome contributions to improve and expand the Rasa Chat Bot. If you'd like to contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Create a new Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
