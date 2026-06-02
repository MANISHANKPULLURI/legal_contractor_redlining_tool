export default function RiskCard(
    { item }: any
) {


    const analysis = item.analysis;


    return (

        <div className="border rounded p-5 mt-5 bg-white text-black">


            <h2 className="text-xl font-bold">

                Clause {item.clause_number}

            </h2>



            <p className="mt-3">

                Risk:

                <b>
                    {" " + analysis.risk_level}
                </b>

            </p>



            <p className="mt-3">

                <b>Original:</b>

                <br />

                {item.clause}

            </p>



            {

                analysis.issues.map(

                    (issue:any,index:number)=>(


                        <div key={index}>


                            <p className="mt-3">

                                <b>Issue:</b>

                                {issue.issue}

                            </p>



                            <p>

                                <b>Why risky:</b>

                                {issue.why_risky}

                            </p>


                        </div>

                    )

                )

            }




            <p className="mt-3">

                <b>Suggestion:</b>

                <br/>

                {analysis.suggestion}

            </p>



            <p className="mt-3">

                <b>AI Rewrite:</b>

                <br/>

                {analysis.rewritten_clause}

            </p>



        </div>

    );

}