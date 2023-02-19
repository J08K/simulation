import type { NextApiRequest, NextApiResponse } from 'next';
import type { SimData } from '@/utils/types';
import { getLatest } from '@/utils/dbConn';

type Data = {
    sim_data : SimData | null,
}

export default async function handler (
    req: NextApiRequest,
    res: NextApiResponse<Data>) {
        if (req.query.collection) {
            return res.status(200).json({sim_data : await getLatest(req.query.collection as string)})
        } else {
            console.log("No collection name was given!");
        }
}