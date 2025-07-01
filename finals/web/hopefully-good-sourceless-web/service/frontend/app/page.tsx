import { Component } from './file';

async function getLatestFlag() {
  const resp = await fetch("http://sourceless_backend/flag", { cache: 'no-store' });
  return resp.text();
}

export default async function Page() {
  const flag = await getLatestFlag();

  async function checkFlag(formData: FormData) {
    "use server";

    if (flag !== formData.get('flag')) {
      throw new Error("Wrong flag!");
    }
  }

  return (
    <>
      <form action={checkFlag}>
        <input type="text" name='flag' />
        <button type="submit">Check flag</button>
        <div>Page will error if the flag is wrong!</div>
      </form>

      <br />

      <Component />
    </>
  );
}
