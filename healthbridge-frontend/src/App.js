import React from 'react';
import { useMsal } from '@azure/msal-react';
import LoginButton from './components/LoginButton';
import FileUpload from './components/FileUpload';

const App = () => {
  const { isAuthenticated } = useMsal();

  return (
    <div>
      {isAuthenticated ? <FileUpload /> : <LoginButton />}
    </div>
  );
};

export default App;