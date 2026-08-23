"use client";

import { useState, useEffect } from "react";

export default function TasksPage() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Tasks</h1>
        {loading ? (
          <p>Loading tasks...</p>
        ) : (
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600">No tasks available at the moment.</p>
          </div>
        )}
      </div>
    </div>
  );
}
