import React from 'react';
import Index, { HeaderProps } from './index.tsx';

export default {
    title: "Header",
    component: Index
};

export const Default = (props: HeaderProps) => <Index {...props} />;
