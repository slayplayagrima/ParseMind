import {
  Dialog as MuiDialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  type DialogProps as MuiDialogProps,
} from '@mui/material';

interface DialogProps extends MuiDialogProps {
  title: string;
  actions?: React.ReactNode;
}

export const Dialog = ({ title, actions, children, ...props }: DialogProps) => (
  <MuiDialog maxWidth="sm" fullWidth {...props}>
    <DialogTitle>{title}</DialogTitle>
    <DialogContent>{children}</DialogContent>
    {actions ? <DialogActions>{actions}</DialogActions> : null}
  </MuiDialog>
);
