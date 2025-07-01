'use client'

import { useActionState } from "react";
import { openFile } from "./actions";

export function Component() {
  const initialState = {
    content: ''
  }
  const [formState, formAction] = useActionState(openFile, initialState)

  return <>
    <form action={formAction}>
      <input type="text" name="file" />
      <button type="submit">Read file</button>
    </form>
    {formState.content}
  </>
}
