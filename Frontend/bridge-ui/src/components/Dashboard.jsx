import React, { useEffect, useState } from 'react';
import { getNamespaces, getResources } from '../api';
import {
  Box, Typography, List, ListItem, ListItemText, CircularProgress, TextField, InputAdornment,
  Card, CardContent, Grid, Toolbar, AppBar, IconButton
} from '@mui/material';
import { styled } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import FolderIcon from '@mui/icons-material/Folder';
import ResourceTable from './ResourceTable';

const DashboardContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(4),
  background: 'linear-gradient(135deg, #2196F3, #9C27B0)', // Gradient background
  minHeight: '100vh',
}));

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  marginBottom: theme.spacing(4),
}));

const StyledSearchField = styled(TextField)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  borderRadius: theme.shape.borderRadius,
  boxShadow: theme.shadows[1],
}));

const Dashboard = () => {
  const [namespaces, setNamespaces] = useState([]);
  const [selectedNamespace, setSelectedNamespace] = useState('');
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchNamespaces = async () => {
      try {
        console.log('Fetching namespaces...');
        const response = await getNamespaces();
        setNamespaces(response.data.namespaces);
        console.log('Namespaces fetched:', response.data.namespaces);
        setSelectedNamespace(response.data.namespaces[0]);
      } catch (error) {
        console.error('Error fetching namespaces:', error);
      }
    };

    fetchNamespaces();
  }, []);

  useEffect(() => {
    const fetchResources = async () => {
      if (!selectedNamespace) return;
      setLoading(true);
      try {
        console.log('Fetching resources for namespace:', selectedNamespace);
        const response = await getResources(selectedNamespace);
        setResources(response.data.resources);
        console.log('Resources fetched:', response.data.resources);
      } catch (error) {
        console.error('Error fetching resources:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchResources();
  }, [selectedNamespace]);

  const handleNamespaceClick = (namespace) => {
    setSelectedNamespace(namespace);
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const filteredResources = resources.filter((resource) =>
    resource.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <DashboardContainer>
      <StyledAppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Dashboard Overview
          </Typography>
          <StyledSearchField
            value={searchQuery}
            onChange={handleSearchChange}
            placeholder="Search..."
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Toolbar>
      </StyledAppBar>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" align="center">
                Namespaces
              </Typography>
              <List>
                {namespaces.map(ns => (
                  <ListItem
                    key={ns}
                    button
                    onClick={() => handleNamespaceClick(ns)}
                    sx={{
                      borderRadius: 1,
                      '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.04)' },
                    }}
                  >
                    <FolderIcon sx={{ marginRight: 1 }} />
                    <ListItemText primary={ns} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={8}>
          {loading ? (
            <CircularProgress />
          ) : (
            <ResourceTable namespace={selectedNamespace} resources={filteredResources} setResources={setResources} />
          )}
        </Grid>
      </Grid>
    </DashboardContainer>
  );
};

export default Dashboard;
