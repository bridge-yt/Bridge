import React from 'react';
import { Box, Typography, Button, Container, Grid, Paper } from '@mui/material';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f4f6f8',
    },
  },
});

const StyledHero = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  color: 'white',
  padding: '2rem',
  textAlign: 'center',
}));

const StyledFeatureCard = styled(Paper)(({ theme }) => ({
  padding: '1rem',
  margin: '1rem 0',
  textAlign: 'center',
  borderRadius: theme.shape.borderRadius,
  boxShadow: theme.shadows[3],
}));

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <ThemeProvider theme={theme}>
      <Box>
        <StyledHero>
          <Typography variant="h3" gutterBottom>
            Welcome to Bridge!
          </Typography>
          <Typography variant="h5" gutterBottom>
            Your Powerful Resource Management Platform
          </Typography>
          <Button variant="contained" color="secondary" onClick={() => navigate('/dashboard')}>
            Get Started
          </Button>
        </StyledHero>

        <Container maxWidth="md" sx={{ marginTop: 4 }}>
          <Typography variant="h4" align="center" gutterBottom>
            Key Features
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <StyledFeatureCard elevation={3}>
                <Typography variant="h6" gutterBottom>
                  Centralized Resource Management
                </Typography>
                <Typography variant="body1">
                  Manage all your resources in one place.
                </Typography>
              </StyledFeatureCard>
            </Grid>
            <Grid item xs={12} sm={6}>
              <StyledFeatureCard elevation={3}>
                <Typography variant="h6" gutterBottom>
                  Multi-Namespace Support
                </Typography>
                <Typography variant="body1">
                  Organize your resources into separate namespaces.
                </Typography>
              </StyledFeatureCard>
            </Grid>
            {/* Add more feature cards as needed */}
          </Grid>
        </Container>

        <Box sx={{ marginTop: 4, padding: 2, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            Ready to get started?
          </Typography>
          <Button variant="outlined" onClick={() => navigate('/dashboard')} sx={{ marginRight: 2 }}>
            Go to Dashboard
          </Button>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default HomePage;
