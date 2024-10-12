import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import PropTypes from 'prop-types';

const ChatInput = ({ message, setMessage, handleSendMessage }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className="chat-input">
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Type your message here..."
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};
ChatInput.propTypes = {
  message: PropTypes.string.isRequired,
  setMessage: PropTypes.func.isRequired,
  handleSendMessage: PropTypes.func.isRequired,
};

const ChatResponse = ({ response }) => (
  <div className="response">
    <h2>Response:</h2>
    <p>{response}</p>
  </div>
);

ChatResponse.propTypes = {
  response: PropTypes.string.isRequired,
};

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSendMessage = async () => {
    if (message.trim() === '') return;
    console.log('Sending message:', message);
    try {
      const res = await axios.post('http://localhost:8000/chat', { message });
      console.log('Received response:', res.data.response);
      setResponse(res.data.response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  // const handleSendMessage = async () => {
  //   if (message.trim() === '') return;
  //   console.log('Sending request to backend...');
  //   try {
  //     const response = await fetch('http://127.0.0.1:8000/chat', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({ message }),
  //     });
  //     const data = await response.json();
  //     console.log('Received response:', data.response);
  //     setResponse(data.response);
  //   } catch (error) {
  //     console.error('Error while sending message:', error);
  //   }
  // };
  
  
  return (
    <div className="App">
      <h1>Azure OpenAI Chat</h1>
      <ChatInput message={message} setMessage={setMessage} handleSendMessage={handleSendMessage} />
      <ChatResponse response={response} />
    </div>
  );
}

export default App;