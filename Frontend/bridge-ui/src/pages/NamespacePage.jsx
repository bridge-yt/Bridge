import React from 'react';
import { useParams } from 'react-router-dom';
import ResourceTable from '../components/ResourceTable';
import { Box, Typography } from '@mui/material';

const NamespacePage = () => {
  const { namespace } = useParams();

  return (
    <Box>
      <Typography variant="h4">Namespace: {namespace}</Typography>
      <ResourceTable namespace={namespace} />
    </Box>
  );
};

export default NamespacePage;
