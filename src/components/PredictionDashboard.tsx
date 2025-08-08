import React from 'react';
import { TrendingUp, TrendingDown, DollarSign, Star, AlertCircle } from 'lucide-react';

interface PredictionData {
  jobTitle: string;
  currentDemand: number;
  year1Growth: number;
  year2Growth: number;
  totalGrowth: number;
  confidenceScore: number;
  salaryRange: string;
  skillsRequired: string[];
  educationPathways: any[];
  monthlyPredictions: any[];
}

interface PredictionDashboardProps {
  predictions: PredictionData[];
  industry: string;
  experience: string;
}

const PredictionDashboard: React.FC<PredictionDashboardProps> = ({ predictions, industry, experience }) => {
  const averageGrowth = predictions.reduce((sum, pred) => sum + pred.totalGrowth, 0) / predictions.length;
  const highGrowthJobs = predictions.filter(pred => pred.totalGrowth > 15).length;
  
  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
      <div className="flex items-center space-x-3 mb-6">
        <div className="p-2 bg-green-100 rounded-lg">
          <TrendingUp className="h-5 w-5 text-green-600" />
        </div>
        <h2 className="text-xl font-semibold text-gray-900">
          2-Year Job Demand Predictions - {industry.charAt(0).toUpperCase() + industry.slice(1)}
        </h2>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600 font-medium">2-Year Growth</p>
              <p className="text-2xl font-bold text-blue-800">+{averageGrowth.toFixed(1)}%</p>
            </div>
            <TrendingUp className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600 font-medium">High Growth Jobs</p>
              <p className="text-2xl font-bold text-green-800">{highGrowthJobs}</p>
            </div>
            <Star className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-50 to-purple-100 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-purple-600 font-medium">Total Jobs Analyzed</p>
              <p className="text-2xl font-bold text-purple-800">{predictions.length}</p>
            </div>
            <AlertCircle className="h-8 w-8 text-purple-600" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-orange-50 to-orange-100 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-orange-600 font-medium">Prediction Period</p>
              <p className="text-2xl font-bold text-orange-800">24 Months</p>
            </div>
            <AlertCircle className="h-8 w-8 text-orange-600" />
          </div>
        </div>
      </div>

      {/* Job Predictions */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Most Demanding Jobs - Next 2 Years</h3>
        {predictions.map((prediction, index) => (
          <div key={index} className="border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all duration-200">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h4 className="text-lg font-semibold text-gray-900 mb-2">{prediction.jobTitle}</h4>
                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <div className="flex items-center space-x-1">
                    <DollarSign className="h-4 w-4" />
                    <span>{prediction.salaryRange}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4" />
                    <span>Confidence: {prediction.confidenceScore}%</span>
                  </div>
                </div>
              </div>
              
              <div className="text-right">
                <div className="space-y-1">
                  <div className={`flex items-center space-x-1 ${
                    prediction.totalGrowth > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {prediction.totalGrowth > 0 ? (
                      <TrendingUp className="h-4 w-4" />
                    ) : (
                      <TrendingDown className="h-4 w-4" />
                    )}
                    <span className="font-bold text-lg">
                      {prediction.totalGrowth > 0 ? '+' : ''}{prediction.totalGrowth}%
                    </span>
                  </div>
                  <p className="text-xs text-gray-500">2-year total growth</p>
                </div>
              </div>
            </div>

            {/* Year-by-Year Growth */}
            <div className="grid grid-cols-2 gap-4 mb-4 p-3 bg-gray-50 rounded-lg">
              <div className="text-center">
                <div className={`flex items-center justify-center space-x-1 ${
                  prediction.year1Growth > 0 ? 'text-blue-600' : 'text-red-600'
                }`}>
                  {prediction.year1Growth > 0 ? (
                    <TrendingUp className="h-4 w-4" />
                  ) : (
                    <TrendingDown className="h-4 w-4" />
                  )}
                  <span className="font-semibold">
                    {prediction.year1Growth > 0 ? '+' : ''}{prediction.year1Growth}%
                  </span>
                </div>
                <p className="text-xs text-gray-500">Year 1 Growth</p>
              </div>
              <div className="text-center">
                <div className={`flex items-center justify-center space-x-1 ${
                  prediction.year2Growth > 0 ? 'text-purple-600' : 'text-red-600'
                }`}>
                  {prediction.year2Growth > 0 ? (
                    <TrendingUp className="h-4 w-4" />
                  ) : (
                    <TrendingDown className="h-4 w-4" />
                  )}
                  <span className="font-semibold">
                    {prediction.year2Growth > 0 ? '+' : ''}{prediction.year2Growth}%
                  </span>
                </div>
                <p className="text-xs text-gray-500">Year 2 Growth</p>
              </div>
            </div>

            {/* Demand Bar */}
            <div className="mb-4">
              <div className="flex justify-between text-sm text-gray-600 mb-1">
                <span>Current Demand</span>
                <span>{prediction.currentDemand}/100</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${prediction.currentDemand}%` }}
                ></div>
              </div>
            </div>

            {/* Skills Preview */}
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Key Skills:</p>
              <div className="flex flex-wrap gap-2">
                {prediction.skillsRequired.slice(0, 4).map((skill, skillIndex) => (
                  <span 
                    key={skillIndex}
                    className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))}
                {prediction.skillsRequired.length > 4 && (
                  <span className="px-3 py-1 bg-gray-100 text-gray-500 rounded-full text-sm">
                    +{prediction.skillsRequired.length - 4} more
                  </span>
                )}
              </div>
            </div>

            {/* Education Pathways Preview */}
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">Recommended Education:</p>
              <div className="space-y-2">
                {prediction.educationPathways.slice(0, 2).map((pathway, pathIndex) => (
                  <div key={pathIndex} className="flex items-center justify-between p-2 bg-blue-50 rounded-lg">
                    <div>
                      <p className="text-sm font-medium text-blue-900">{pathway.title}</p>
                      <p className="text-xs text-blue-600">{pathway.institution} • {pathway.duration}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-blue-700 font-medium">{pathway.alignment}% match</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PredictionDashboard;