import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';
import App from './App';
import { GroupProvider } from './contexts/GroupContext';
import { PostProvider } from './contexts/PostContext';
import { UserProvider } from './contexts/UserContext';

const root = ReactDOM.createRoot(document.getElementById('root'))

root.render(
  <Router>
    <UserProvider>
    <PostProvider>
    <GroupProvider>
      <App />
    </GroupProvider>
    </PostProvider>
    </UserProvider>
  </Router>
)
