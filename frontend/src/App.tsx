// src/App.tsx
import React, { useState, useEffect } from "react";

type GenerateRequest = {
  prompt: string;
  height: number;
  width: number;
  num_inference_steps: number;
  seed: number;
};

const App: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [height, setHeight] = useState(512);
  const [width, setWidth] = useState(512);
  const [numSteps, setNumSteps] = useState(9);
  const [seed, setSeed] = useState(42);

  const [taskId, setTaskId] = useState("");
  const [taskStatus, setTaskStatus] = useState("");

  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    return () => {
      if (imageUrl) {
        URL.revokeObjectURL(imageUrl);
      }
    };
  }, [imageUrl]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!prompt.trim()) {
      setError("prompt를 입력하세요.");
      return;
    }

    setError(null);

    try {
      const payload: GenerateRequest = {
        prompt,
        height,
        width,
        num_inference_steps: numSteps,
        seed,
      };

      const res = await fetch(`/api/v1/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`이미지 생성 요청 실패: ${res.status}`);
      }

      setIsGenerating(true);

      const data = await res.json();
      setTaskId(data.task_id);

    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : "알 수 없는 오류입니다.");
    } finally {
      setIsGenerating(false);
    }
  };

  const getGeneratedImage = async () => {

    setError(null);

    if(isGenerating) {
      throw new Error("이미지 생성 중입니다. 잠시만 기다려주세요.");
    }

    try {
      const res = await fetch('/api/v1/tasks/' + taskId + '/result', {
        method: "GET",
      });

      if (!res.ok) {
        throw new Error(`이미지 생성 결과 요청 실패: ${res.status}`);
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);

      if (imageUrl) URL.revokeObjectURL(imageUrl);
      setImageUrl(url);
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : "알 수 없는 오류입니다.");
    } finally {
      setIsGenerating(false);
    }
  };

  const getLatestTaskId = async () => {

    setError(null);

    try {
      const res = await fetch('/api/v1/tasks', {
        method: "GET",
      });
    
      if(!res.ok) {
        throw new Error(`태스크 목록 요청 실패: ${res.status}`);
      }
      
      const data = await res.json();
      if(data && data.length > 0) {
        if(data[0].status === 'completed') {
          setIsGenerating(false);
        }
        else if(data[0].status === 'failed') {
          setIsGenerating(false);
          throw new Error("태스크가 실패했습니다.");
        }
        setTaskId(data[0].task_id);
        setTaskStatus(data[0].status);
      } else {
        throw new Error("태스크가 없습니다.");
      }
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : "알 수 없는 오류입니다.");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>Simple Image Generator</h1>

      <form onSubmit={handleGenerate} style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: 500 }}>
        
        <label>
          Prompt
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={3}
            style={{ width: "100%" }}
          />
        </label>

        <label>
          Height
          <input type="number" value={height} onChange={(e) => setHeight(Number(e.target.value))} />
        </label>

        <label>
          Width
          <input type="number" value={width} onChange={(e) => setWidth(Number(e.target.value))} />
        </label>

        <label>
          Num inference steps
          <input type="number" value={numSteps} onChange={(e) => setNumSteps(Number(e.target.value))} />
        </label>

        <label>
          Seed
          <input type="number" value={seed} onChange={(e) => setSeed(Number(e.target.value))} />
        </label>

        <button type="submit" disabled={isGenerating}>
          {isGenerating ? "생성 중..." : "이미지 생성"}
        </button>
      </form>

      <button onClick={getLatestTaskId} style={{ marginTop: "10px" }}>최신 태스크 ID 가져오기</button>
      <button onClick={getGeneratedImage} style={{ marginTop: "10px" }}>태스크 ID로 이미지 가져오기</button>

      <div>
        <p>{taskId.length > 0 ? "태스크 ID: " + taskId : "태스크 ID: 태스크 조회 되지 않음"}</p>
        <p>{taskStatus.length > 0 ? "태스크 상태: " + taskStatus : "태스크 상태: 태스크 조회 되지 않음"}</p>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div style={{ marginTop: "20px" }}>
        {imageUrl ? (
          <img src={imageUrl} alt="generated" style={{ maxWidth: "100%" }} />
        ) : (
          <p>아직 생성된 이미지 없음.</p>
        )}
      </div>
    </div>
  );
};

export default App;
