// App.js
import React from 'react';
import { Route, Routes, Link } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme'; // Import your custom theme
import HomePage from './pages/HomePage';
import Dashboard from './components/Dashboard';
import NamespacePage from './pages/NamespacePage';

// ... your other components

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline /> {/* Normalize styles for consistent rendering across browsers */}
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/namespace/:namespace" element={<NamespacePage />} />
        </Routes>
      </div>
    </ThemeProvider>
  );
}

export default App;
