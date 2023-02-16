import type { NextApiRequest, NextApiResponse } from 'next';

type Data = {
    is_connected: boolean,
}

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<Data>
  ) {
    console.log("Hello, World!")
    return res.status(200).json({ is_connected: true })
  }
  