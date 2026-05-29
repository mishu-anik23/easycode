import * as vscode from 'vscode';
import { sendChatRequest } from './api';

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.startChat', async () => {
      const prompt = await vscode.window.showInputBox({ prompt: 'Ask EasyCode' });
      if (!prompt) return;
      const response = await sendChatRequest(prompt);
      vscode.window.showInformationMessage(response.reply);
    })
  );
}

export function deactivate() {}
