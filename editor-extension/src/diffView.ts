import * as vscode from 'vscode';

export function showDiffView(diff: string) {
  const doc = vscode.workspace.openTextDocument({ content: diff, language: 'diff' });
  doc.then(document => vscode.window.showTextDocument(document, { preview: false }));
}
