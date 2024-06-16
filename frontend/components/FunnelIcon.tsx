import React from 'react';

type FunnelIconProps = {
  toggled: boolean;
};

const FunnelIcon: React.FC<FunnelIconProps> = ({ toggled }) => (
  <svg
    width="14"
    height="14"
    viewBox="0 0 188 173"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M79.767,11.043167,95.3,307.1-0,56.4751-48.733,-21.2051-0.597,-53.8811-62.639,-74.696Z"
      stroke="#63AAAF"
      strokeWidth="20"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill={toggled ? '#63AAAF' : 'transparent'}
    />
  </svg>
);

export default FunnelIcon;
