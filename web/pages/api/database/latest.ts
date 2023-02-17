import type { NextApiRequest, NextApiResponse } from 'next';
import type { SimData } from '@/utils/types';
import { getLatest } from '@/utils/dbConn';

type Data = {
    sim_data : SimData | null,
}

export default async function handler (
    req: NextApiRequest,
    res: NextApiResponse<Data>) {
        console.log(req.method)
        if (req.body) {
            console.log(req.body.collection_name)
            await getLatest(req.body.collection_name)
            return res.status(200).json({sim_data : await getLatest(req.body.collection_name)})
        }
}