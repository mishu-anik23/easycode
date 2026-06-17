import * as vscode from 'vscode';

export async function showDiffView(diff: string) {
  const document = await vscode.workspace.openTextDocument({ content: diff, language: 'diff' });
  await vscode.window.showTextDocument(document, { preview: false });
}
