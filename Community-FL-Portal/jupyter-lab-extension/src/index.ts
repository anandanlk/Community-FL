import {
    JupyterFrontEnd, 
    JupyterFrontEndPlugin
  } from '@jupyterlab/application';
  
  import {
    ILauncher
  } from '@jupyterlab/launcher';
  
  const extension: JupyterFrontEndPlugin<void> = {
    id: 'communityfl',
    autoStart: true,
    requires: [ILauncher],
    activate: (app: JupyterFrontEnd, launcher: ILauncher) => {
      console.log('JupyterLab extension communityfl button is activated!');
  
      const command = 'open-url:open';
  
      app.commands.addCommand(command, {
        label: 'Community FL',
        execute: () => {
          window.open('http://145.100.135.10:3000', '_blank');
        },
        iconClass: 'jp-Icon-20 jp-HomeIcon'
      });
  
      launcher.add({
        command: command,
        category: 'Other'
      });
    }
  };
  
  export default extension;
  