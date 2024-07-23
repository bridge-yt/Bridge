import React, { useEffect, useState } from 'react';
import { getResources, deleteResource } from '../api';
import { List, ListItem, ListItemText, Button } from '@mui/material';

const ResourceList = ({ namespace }) => {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResources = async () => {
      setLoading(true);
      try {
        console.log('Fetching resources for namespace:', namespace);
        const response = await getResources(namespace);
        setResources(response.data.resources);
        console.log('Resources fetched:', response.data.resources);
      } catch (error) {
        setError(error);
        console.error('Error fetching resources:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchResources();
  }, [namespace]);

  const handleDelete = async (name) => {
    try {
      console.log('Deleting resource:', name);
      await deleteResource(namespace, name);
      setResources(resources.filter(resource => resource.name !== name));
      console.log('Resource deleted successfully');
    } catch (error) {
      setError(error);
      console.error('Error deleting resource:', error);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <List>
      {resources.map(resource => (
        <ListItem key={resource.name || resource.id}>
          <ListItemText primary={resource.name} secondary={resource.arn} />
          <Button variant="contained" color="secondary" onClick={() => handleDelete(resource.name)}>
            Delete
          </Button>
        </ListItem>
      ))}
    </List>
  );
};

export default ResourceList;
