"use client";

import { useState } from "react";

import RiskCard from "@/components/RiskCard";


export default function Home() {


  const [message, setMessage] = useState("");

  const [answer, setAnswer] = useState<any>(null);


  const [file, setFile] = useState<File | null>(null);

  const [review, setReview] = useState<any>(null);


  const [redlineFile, setRedlineFile] = useState("");


  // NEW: query with uploaded document

  const [reviewQuery, setReviewQuery] = useState("");





  // -------------------------
  // Normal RAG Chat
  // -------------------------

  async function sendMessage() {


    const response = await fetch(

      "http://127.0.0.1:8000/chat",

      {

        method: "POST",

        headers: {

          "Content-Type": "application/json"

        },


        body: JSON.stringify({

          message: message

        })

      }

    );



    const data = await response.json();


    setAnswer(

      data.answer

    );

  }






  // -------------------------
  // Agentic RAG Review
  // File + User Instruction
  // -------------------------

  async function uploadContract() {


    if (!file) {


      alert("Please select contract file");


      return;


    }





    const formData = new FormData();




    formData.append(

      "file",

      file

    );




    // NEW: send query also

    formData.append(

      "query",

      reviewQuery || "Review this contract"

    );





    const response = await fetch(

      "http://127.0.0.1:8000/review",

      {

        method: "POST",

        body: formData

      }

    );




    const data = await response.json();




    setReview(

      data.review

    );




    setRedlineFile(

      data.redline_file

    );


  }







  // -------------------------
  // Download Redline
  // -------------------------

  function downloadRedline() {


    window.open(


      `http://127.0.0.1:8000/download/${redlineFile}`,


      "_blank"


    );


  }








  return (

    <main className="p-10">


      <h1 className="text-4xl font-bold">

        LegalContractor AI

      </h1>








      {/* CHAT */}


      <section className="mt-10">


        <h2 className="text-2xl font-bold">

          Ask Legal Question

        </h2>



        <input

          className="border p-3 w-96 text-black mt-4 rounded"


          placeholder="Ask legal question..."


          value={message}


          onChange={(e) =>

            setMessage(e.target.value)

          }

        />




        <button

          className="ml-4 bg-blue-600 text-white p-3 rounded"


          onClick={sendMessage}

        >

          Ask AI

        </button>


      </section>







      {answer && (


        <pre className="mt-6 bg-gray-100 text-black p-5 rounded">


          {

            JSON.stringify(

              answer,

              null,

              2

            )

          }


        </pre>


      )}









      {/* CONTRACT UPLOAD */}


      <section className="mt-14">


        <h2 className="text-2xl font-bold">

          Upload Contract

        </h2>






        {/* NEW QUERY BOX */}


        <input


          className="border p-3 w-96 text-black mt-4 rounded block"


          placeholder="Optional: e.g. Check only liability risks"


          value={reviewQuery}



          onChange={(e) =>


            setReviewQuery(

              e.target.value

            )


          }


        />







        <input


          className="mt-5"


          type="file"


          onChange={(e) =>


            setFile(

              e.target.files?.[0] || null

            )


          }


        />







        <button


          className="ml-4 bg-green-600 text-white p-3 rounded"


          onClick={uploadContract}


        >


          Review Contract


        </button>



      </section>








      {/* REVIEW OUTPUT */}


      {review && (


        <section className="mt-10">


          <h2 className="text-3xl font-bold">

            Contract Risk Report

          </h2>





          {

            review.risks.map(

              (item:any)=>(


                <RiskCard


                  key={item.clause_number}


                  item={item}


                />

              )

            )

          }






          <button


            className="mt-8 bg-purple-600 text-white p-3 rounded"


            onClick={downloadRedline}

          >


            Download Redlined DOCX


          </button>




        </section>


      )}




    </main>

  );

}