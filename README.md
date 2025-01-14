# System Control via Gestures and Voice Commands

This project is a comprehensive solution for controlling system functionalities using hand gestures, eye gestures, and voice commands. It aims to provide a hands-free and interactive way of operating devices, improving accessibility and efficiency.

## Features

- **Hand Gesture Control**: Use predefined hand gestures to perform actions like cursor movement and system navigation.
- **Eye Gesture Control**: Track eye movements to control the cursor and perform specific tasks.
- **Voice Command Integration**: Execute commands and control the system using natural language voice inputs.
- **Multi-Modal Interface**: Offers a choice between different modes of control (gesture or voice).

## Technologies Used

- **Programming Language**: Python
- **Libraries**:
  - OpenCV: For gesture and eye tracking
  - SpeechRecognition: For voice command processing
  - PyAutoGUI: For simulating keyboard and mouse inputs
  - TensorFlow/Keras: For gesture recognition (if applicable)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/system-control-gestures-voice.git
   cd system-control-gestures-voice
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure your system has a functional webcam and microphone.

## Usage

1. Run the main program:
   ```bash
   python front.py
   ```

2. Choose the mode of control when prompted:
   - Chatbot Mode
   - Cursor Control Using Hand Gestures
   - Cursor Control Using Eye Gestures
   - System Control Using Voice Commands

3. When you choose option Chatbot Mode You must say wake up command when it shows LISTENING [wake up command is : Open Chatbot Mode]
   - To exit [Exit Chatbot Mode]

       
4. Follow the on-screen instructions to interact with the system.

## Project Structure

- `front.py`: The entry point of the program.
- `test4/`: Contains modules for hand gesture recognition.
- `eye/`: Includes scripts for eye gesture tracking.
- `voice/`: Houses voice command processing logic.
- `README.md`: Documentation for the project.

## Future Improvements

- Enhance gesture recognition accuracy using advanced neural networks.
- Add support for custom voice commands.
- Optimize performance for low-resource devices.
- Integrate with IoT devices for broader control applications.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For queries or suggestions, contact:
- **Name**: Syed Roshan
- **Email**: toroshaninbox1@gmail.com
- **GitHub**: [syed-roshan01](https://github.com/syed-roshan01)
