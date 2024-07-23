// theme.js
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light', // Or 'dark' for dark mode
    primary: {
      main: '#1976d2', // Your primary color
    },
    secondary: {
      main: '#f50057', // Your secondary color
    },
    background: {
      default: '#fff',
      paper: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif', // Choose your preferred font family
  },
});

export default theme;
