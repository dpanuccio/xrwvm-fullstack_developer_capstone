import LoginPanel from "./components/Login/Login";
import Register from './components/Register/Register';
import Dealers from './components/Dealers/Dealers';
import Dealer from "./components/Dealers/Dealer";
import PostReview from './components/Dealers/PostReview'; // Import PostReview

import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} /> {/* Added Register route */}
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      <Route path="/postreview/:id" element={<PostReview />} /> {/* Added PostReview route */}
    </Routes>
  );
}

export default App;
