import type { NextApiRequest, NextApiResponse } from 'next';
import type { SimData } from '@/utils/types';
import { getLatest, getSpecific } from '@/utils/dbConn';

type Data = {
    sim_data : SimData | null,
}

export default async function handler (
    req: NextApiRequest,
    res: NextApiResponse<Data>) {
        if (req.query.collection) {
            if (Number(req.query.time) === -1) {
                return res.status(200).json({sim_data : await getLatest(req.query.collection as string)})
            } else if (Number(req.query.time) >= 0) {
                return res.status(200).json({sim_data : await getSpecific(req.query.collection as string, Number(req.query.time))});
            } else {
                console.log("Invalid time was given!")
            }
        } else {
            console.log("No collection name was given!");
        }
}