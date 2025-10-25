"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { Eye, EyeOff, Mail, Lock, User } from "lucide-react";
import { useRouter } from "next/navigation";
import axios from 'axios';

// Convert mm to px (1mm ≈ 3.78px)
const mmToPx = (mm: number) => `${Math.round(mm * 3.78)}px`

interface AuthFormData {
  name?: string;
  email: string;
  password: string;
}

export function AuthForm() {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const router = useRouter();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AuthFormData>();

  const toggleMode = () => {
    setIsLogin(!isLogin);
    reset();
  };

  const onSubmit = async (data: AuthFormData) => {
    setIsSubmitting(true);
    setErrorMessage(""); // Reset error message on submit

    try {
      let response;
      if (isLogin) {
        // 🟢 تعديل هنا: نستخدم URLSearchParams بدلاً من JSON
        const params = new URLSearchParams();
        params.append("username", data.email);
        params.append("password", data.password);

        response = await axios.post(
          "http://localhost:8000/api/v1/users/users/login",
          params,
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          }
        );
      } else {
        // التسجيل عادي باستخدام JSON
        response = await axios.post("http://localhost:8000/api/v1/users/users/create", {
          name: data.name,
          email: data.email,
          password: data.password,
        });
      }

      if (response.status === 200) {
        if (isLogin) {
          localStorage.setItem("access_token", response.data.access_token);
        }
        router.push("/assistant");
      }
    } catch (error) {
      setErrorMessage("An error occurred, please try again.");
      console.error("Authentication error:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-white">
      <div className="w-full bg-white rounded-lg shadow-sm border border-gray-100 p-8" style={{ maxWidth: mmToPx(110) }}>
        <div className="flex justify-center mb-6">
          <img
            src="/logo.png"
            alt="AI Programming Assistant"
            className="h-12 w-auto"
            onError={(e) => {
              e.currentTarget.src =
                "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' fill='%231a365d' rx='20' ry='20'/%3E%3Ctext x='50' y='50' fontFamily='Arial' fontSize='40' fill='white' textAnchor='middle' dominantBaseline='middle'%3EAI%3C/text%3E%3C/svg%3E";
            }}
          />
        </div>

        <h1 className="text-xl font-semibold text-center text-[#1a365d] mb-6">
          {isLogin ? "Welcome back" : "Create your account"}
        </h1>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {!isLogin && (
            <div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                  <User size={16} />
                </div>
                <input
                  id="name"
                  type="text"
                  className={`block w-full pl-10 pr-3 py-2 border ${errors.name ? "border-red-300" : "border-gray-200"} rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white`}
                  style={{ height: mmToPx(10) }}
                  placeholder="Full Name"
                  {...register("name", {
                    required: !isLogin ? "Name is required" : false,
                  })}
                />
              </div>
              {errors.name && <p className="mt-1 text-xs text-red-600">{errors.name.message}</p>}
            </div>
          )}

          <div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                <Mail size={16} />
              </div>
              <input
                id="email"
                type="email"
                className={`block w-full pl-10 pr-3 py-2 border ${errors.email ? "border-red-300" : "border-gray-200"} rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white`}
                style={{ height: mmToPx(10) }}
                placeholder="Email address"
                {...register("email", {
                  required: "Email is required",
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: "Invalid email address",
                  },
                })}
              />
            </div>
            {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email.message}</p>}
          </div>

          <div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                <Lock size={16} />
              </div>
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                className={`block w-full pl-10 pr-10 py-2 border ${errors.password ? "border-red-300" : "border-gray-200"} rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white`}
                style={{ height: mmToPx(10) }}
                placeholder="Password"
                {...register("password", {
                  required: "Password is required",
                  minLength: {
                    value: 6,
                    message: "Password must be at least 6 characters",
                  },
                })}
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
            {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password.message}</p>}
          </div>

          {isLogin && (
            <div className="flex items-center justify-end">
              <a href="#" className="text-xs text-[#1a365d] hover:text-blue-800">
                Forgot your password?
              </a>
            </div>
          )}

          <div className="pt-2">
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-[#1a365d] hover:bg-[#152c4a] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-colors duration-200"
              style={{ height: mmToPx(11) }}
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <div className="flex items-center">
                  <svg
                    className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  {isLogin ? "Logging in..." : "Creating account..."}
                </div>
              ) : (
                <span>{isLogin ? "Login" : "Sign Up"}</span>
              )}
            </button>
          </div>
        </form>

        <div className="mt-6 text-center">
          <p className="text-xs text-gray-600">
            {isLogin ? "Don't have an account?" : "Already have an account?"}
            <button
              type="button"
              onClick={toggleMode}
              className="ml-1 font-medium text-[#1a365d] hover:text-blue-800 focus:outline-none"
            >
              {isLogin ? "Sign up" : "Login"}
            </button>
          </p>
        </div>

        {errorMessage && <p className="mt-3 text-xs text-red-600 text-center">{errorMessage}</p>}
      </div>
    </div>
  );
}



