import React, { useEffect, useState } from 'react';
import { getNamespaces } from '../api';
import { List, ListItem, ListItemText } from '@mui/material';

const NamespaceList = () => {
  const [namespaces, setNamespaces] = useState([]);

  useEffect(() => {
    console.log("Fetching namespaces...");
    getNamespaces()
      .then(response => {
        console.log("Namespaces fetched:", response.data.namespaces);
        setNamespaces(response.data.namespaces);
      })
      .catch(error => {
        console.error("Error fetching namespaces:", error);
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
