import React, { useEffect, useState } from 'react';
import { getNamespaces } from '../api';
import { List, ListItem, ListItemText } from '@mui/material';

const NamespaceList = () => {
  const [namespaces, setNamespaces] = useState([]);

  useEffect(() => {
    getNamespaces().then(response => {
      setNamespaces(response.data.namespaces);
    });
  }, []);

  return (
    <List>
      {namespaces.map(ns => (
        <ListItem key={ns} button component="a" href={`/namespace/${ns}`}>
          <ListItemText primary={ns} />
        </ListItem>
      ))}
    </List>
  );
};

export default NamespaceList;
