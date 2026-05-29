import * as vscode from 'vscode';

export function showChatPanel(message: string) {
  const panel = vscode.window.createWebviewPanel('easycodeChat', 'EasyCode Chat', vscode.ViewColumn.One, {});
  panel.webview.html = `<html><body><h1>EasyCode</h1><p>${message}</p></body></html>`;
}
