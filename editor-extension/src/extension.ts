import * as path from 'path';
import * as vscode from 'vscode';
import {
  sendChatRequest,
  searchCode,
  generateDiff,
  applyDiff,
} from './api';
import { showChatPanel } from './chatPanel';
import { showDiffView } from './diffView';

function getWorkspaceRoot(): string | undefined {
  const folder = vscode.workspace.workspaceFolders?.[0];
  return folder?.uri.fsPath;
}

function getSelectedFile(): string | undefined {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    return undefined;
  }
  const workspaceRoot = getWorkspaceRoot();
  if (!workspaceRoot) {
    return undefined;
  }
  const fileUri = editor.document.uri;
  if (fileUri.scheme !== 'file') {
    return undefined;
  }
  return path.relative(workspaceRoot, fileUri.fsPath);
}

export function activate(context: vscode.ExtensionContext) {
  const output = vscode.window.createOutputChannel('EasyCode');
  context.subscriptions.push(output);

  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.startChat', async () => {
      const prompt = await vscode.window.showInputBox({ prompt: 'Ask EasyCode' });
      if (!prompt) {
        return;
      }

      const filePath = getSelectedFile();
      const selectedFiles = filePath ? [filePath] : [];
      const response = await sendChatRequest(prompt, selectedFiles);
      output.appendLine(`Chat request: ${prompt}`);
      output.appendLine(`Reply:\n${response.reply}`);
      showChatPanel(response.reply);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.searchCode', async () => {
      const query = await vscode.window.showInputBox({ prompt: 'Search the repository' });
      if (!query) {
        return;
      }

      const results = await searchCode(query);
      if (results.length === 0) {
        vscode.window.showInformationMessage('No matches found.');
        return;
      }

      const selection = await vscode.window.showQuickPick(results, {
        placeHolder: 'Search results',
      });
      if (selection) {
        vscode.window.showInformationMessage(selection);
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.generateDiff', async () => {
      const goal = await vscode.window.showInputBox({ prompt: 'Describe the change you want to make' });
      if (!goal) {
        return;
      }

      const filePath = getSelectedFile();
      const files = filePath ? [filePath] : [];
      const result = await generateDiff(goal, files);
      showDiffView(result.diff);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.applyDiff', async () => {
      let diff = '';
      const activeEditor = vscode.window.activeTextEditor;
      if (activeEditor?.document.languageId === 'diff') {
        diff = activeEditor.document.getText();
      }

      if (!diff) {
        const input = await vscode.window.showInputBox({ prompt: 'Paste the unified diff to apply' });
        if (!input) {
          return;
        }
        diff = input;
      }

      const result = await applyDiff(diff);
      vscode.window.showInformationMessage(`Diff application status: ${result.status}`);
    })
  );
}

export function deactivate() {}
