import * as vscode from 'vscode';

export function registerCommands(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.openDiffView', () => {
      vscode.window.showInformationMessage('EasyCode diff view is not implemented yet.');
    })
  );
}
