import React from 'react';
import { useParams } from 'react-router-dom';

const NamespacePage = () => {
  const { namespace } = useParams();

  return (
    <div>
      <h1>Namespace: {namespace}</h1>
    </div>
  );
};

export default NamespacePage;
