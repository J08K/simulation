import type { NextApiRequest, NextApiResponse } from 'next';
import { checkStatus } from '@/utils/dbConn';

type Data = {
    is_connected: boolean,
}

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<Data>
  ) {
    return res.status(200).json({ is_connected: await checkStatus() }) // TODO Add more statusses
  }
  