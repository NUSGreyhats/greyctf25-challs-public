"use server";

import { readFile } from "fs/promises";

export async function openFile(currentState: { content: string }, formData: FormData) {
  const fileName = formData.get('file');
  if (typeof fileName !== 'string') {
    throw new Error("Invalid file!");
  }

  try {
    const data = await readFile(fileName, 'utf-8');
    return { content: data };
  } catch {
    return { content: "Error retrieving data" };
  }
}
