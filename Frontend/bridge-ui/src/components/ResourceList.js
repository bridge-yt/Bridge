import React, { useEffect, useState } from 'react';
import { getResources, deleteResource } from '../api';
import { List, ListItem, ListItemText, Button } from '@mui/material';

const ResourceList = ({ namespace }) => {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    getResources(namespace).then(response => {
      setResources(response.data.resources);
    });
  }, [namespace]);

  const handleDelete = (name) => {
    deleteResource(namespace, name).then(() => {
      setResources(resources.filter(resource => resource.name !== name));
    });
  };

  return (
    <List>
      {resources.map(resource => (
        <ListItem key={resource.name}>
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
