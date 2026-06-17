import * as path from 'path';
import * as vscode from 'vscode';
import {
  sendChatRequest,
  searchCode,
  searchFolderLocal,
  searchFolderGoogleDrive,
  searchFolderDropbox,
  getGoogleDriveAuthUrl,
  getDropboxAuthUrl,
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
      try {
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
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`EasyCode chat failed: ${message}`);
        output.appendLine(`EasyCode chat failed: ${message}`);
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.searchCode', async () => {
      try {
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
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`EasyCode search failed: ${message}`);
        output.appendLine(`EasyCode search failed: ${message}`);
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.folderSearch', async () => {
      try {
        const sourceOption = await vscode.window.showQuickPick(
          [
            { label: 'Local Folder', description: 'Search files in a local folder' },
            { label: 'Google Drive', description: 'Search files in Google Drive' },
            { label: 'Dropbox', description: 'Search files in Dropbox' },
          ],
          { placeHolder: 'Select search source' }
        );

        if (!sourceOption) {
          return;
        }

        const query = await vscode.window.showInputBox({ prompt: 'Enter search query' });
        if (!query) {
          return;
        }

        let results: string[] = [];

        if (sourceOption.label === 'Local Folder') {
          const folderUri = await vscode.window.showOpenDialog({
            canSelectFolders: true,
            canSelectFiles: false,
            canSelectMany: false,
            title: 'Select folder to search',
          });

          if (!folderUri || folderUri.length === 0) {
            return;
          }

          const folderPath = folderUri[0].fsPath;
          results = await searchFolderLocal(folderPath, query);
        } else if (sourceOption.label === 'Google Drive') {
          try {
            const authData = await getGoogleDriveAuthUrl();
            vscode.window.showInformationMessage(
              'Google Drive authentication required. Opening browser...',
              'Open Auth URL'
            );

            // In a real implementation, you would open the auth URL and handle the callback
            const authToken = await vscode.window.showInputBox({
              prompt: 'Enter Google Drive auth token (after authentication)',
              password: true,
            });

            if (!authToken) {
              return;
            }

            results = await searchFolderGoogleDrive(query, authToken);
          } catch (error) {
            vscode.window.showErrorMessage('Google Drive authentication not available yet');
          }
        } else if (sourceOption.label === 'Dropbox') {
          try {
            const authData = await getDropboxAuthUrl();
            vscode.window.showInformationMessage(
              'Dropbox authentication required. Opening browser...',
              'Open Auth URL'
            );

            // In a real implementation, you would open the auth URL and handle the callback
            const authToken = await vscode.window.showInputBox({
              prompt: 'Enter Dropbox auth token (after authentication)',
              password: true,
            });

            if (!authToken) {
              return;
            }

            results = await searchFolderDropbox(query, authToken);
          } catch (error) {
            vscode.window.showErrorMessage('Dropbox authentication not available yet');
          }
        }

        if (results.length === 0) {
          vscode.window.showInformationMessage('No matches found.');
          return;
        }

        const selection = await vscode.window.showQuickPick(results, {
          placeHolder: 'Search results',
        });

        if (selection) {
          vscode.window.showInformationMessage(`Selected: ${selection}`);
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`EasyCode folder search failed: ${message}`);
        output.appendLine(`EasyCode folder search failed: ${message}`);
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.generateDiff', async () => {
      try {
        const goal = await vscode.window.showInputBox({ prompt: 'Describe the change you want to make' });
        if (!goal) {
          return;
        }

        const filePath = getSelectedFile();
        const files = filePath ? [filePath] : [];
        const result = await generateDiff(goal, files);
        await showDiffView(result.diff);
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`EasyCode diff generation failed: ${message}`);
        output.appendLine(`EasyCode diff generation failed: ${message}`);
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('easycode.applyDiff', async () => {
      try {
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
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`EasyCode apply diff failed: ${message}`);
        output.appendLine(`EasyCode apply diff failed: ${message}`);
      }
    })
  );
}

export function deactivate() {}
