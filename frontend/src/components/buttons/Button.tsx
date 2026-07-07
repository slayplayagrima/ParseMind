import { Button as MuiButton, type ButtonProps as MuiButtonProps } from '@mui/material';

export type ButtonProps = MuiButtonProps;

export const Button = ({ children, sx, ...props }: ButtonProps) => (
  <MuiButton disableElevation {...props} sx={{ borderRadius: '9999px', ...sx }}>
    {children}
  </MuiButton>
);
