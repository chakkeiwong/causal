/* 
 * This program opens a text file and transfers its non-empty lines to a user-defined
 * output file.
 * NOTE: See the below comment involving getline() function !!! 
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>
#include "prompt.h"
#include "strutils.h"

using namespace std;


bool exists (string **& FeatureValues, int i, string word)
{
	for(int j = 0; j<15; j++)
	{
		if(FeatureValues[i][j]==word)
			return true;
	}
	return false;
}

int addFeatureValue (string **& FeatureValues, int i, string word)
{
	for(int j = 0; j<15; j++)
	{
		if(FeatureValues[i][j]=="CTRL")
		{
			FeatureValues[i][j]=word;
			return 0;
		}			
	}	
}

void printFeatureValues (const vector<string> & Features, string **& FeatureValues)
{
	for(int i=0; i<15; i++)
	{
		cout<<endl<<"Feature "<<Features[i]<<":"<<endl;
		for(int j = 0; j<15; j++)
		{
			if(FeatureValues[i][j]!="CTRL")
			{
				cout<<FeatureValues[i][j]<<";";
			}				
		}
		cout<<endl;
	}		
}

void printTheTable(const vector<vector<string>> & theTable)
{
	for(int i=0; i<theTable.size(); i++)
	{
		cout<<"Row "<<i<<":"<<endl;
		for(int j = 0; j<theTable[i].size()-1; j++)
		{
			cout<<theTable[i][j]<<";";
		}
		cout<<theTable[i][theTable[i].size()-1];
		cout<<endl<<endl;
	}
}

void processFile(ifstream &input, ofstream &output)
{
	string strLine, word;
	vector<string> Features;
	
	getline(input,strLine);
	StripWhite(strLine);
	ToUpper(strLine);
	unsigned int smileys = 0, index = 0, length, firstIndex = 0;
	string searchPattern = ",";
    if (strLine != "")
    {
		cout<<strLine<<endl<<endl<<endl;
			    length = strLine.length();
		
		while (index < length)
		{
			index = strLine.find(",", index);
		
			if (index != string::npos)
			{
				index += searchPattern.length();
				word = strLine.substr(firstIndex, index-firstIndex-1);
				Features.push_back(word);
				cout<<"The found word: "<<word<<endl;
				firstIndex = index;
				smileys++;
			}
		}
		word = strLine.substr(firstIndex);
		Features.push_back(word);
		cout<<"The found word: "<<word<<endl;
		cout<<"Number of commas is "<<smileys<<endl;
    }

	cout<<endl<<endl<<"The features vector is:"<<endl;
	for(int i =0; i<Features.size(); i++)
		cout<<Features[i]<<endl;
	//system("pause");


	//DEALING WITH FEATURE VALUES
	string ** FeatureValues = new string * [15];
	for(int i =0; i<15; i++)
	{
		FeatureValues[i] = new string [15];
		for(int j = 0; j<15; j++)
		{
			FeatureValues[i][j]="CTRL";
		}
	}
	

	vector<vector<string>> theTable;
	int lineCount = 0;
	while (getline(input,strLine))
	{
		StripWhite(strLine);
		ToUpper(strLine);
		lineCount++;
		//cout<<endl<<endl<<"processing line "<<lineCount<<endl;
		vector<string> row;
		unsigned int smileys = 0, index = 0, length, firstIndex = 0;
		string searchPattern = ",";
		if (strLine != "")
		{
			//cout<<strLine<<endl;
			length = strLine.length();
		
			while (index < length)
			{
				if(strLine.at(firstIndex) == '"')
				{
					index = strLine.find("\"", index+1);
					if (index != string::npos)
					{
						index += searchPattern.length();
						word = strLine.substr(firstIndex+1, index-firstIndex-2);
						StripWhite(word);
						if(word=="")
							word = "CTRL";
						//cout<<"The found word: "<<word<<endl;
						row.push_back(word);
						//cout<<"firstIndex="<<firstIndex<<", index="<<index<<endl;
						index++;
						firstIndex = index;
						if(!exists(FeatureValues,smileys,word))
							addFeatureValue(FeatureValues,smileys,word);
						smileys++;
					}
					//system("pause");
				}
				else
				{
					index = strLine.find(",", index);
					if (index != string::npos)
					{
						index += searchPattern.length();
						word = strLine.substr(firstIndex, index-firstIndex-1);
						StripWhite(word);
						if(word=="")
							word = "CTRL";
						//cout<<"The found word: "<<word<<endl;
						row.push_back(word);
						firstIndex = index;
						if(!exists(FeatureValues,smileys,word))
							addFeatureValue(FeatureValues,smileys,word);
						smileys++;
					}
				}
				
			}//while

			word = strLine.substr(firstIndex);	
			StripWhite(word);
			//cout<<"The found word: "<<word<<endl;
			row.push_back(word);
			if(!exists(FeatureValues,smileys,word))
							addFeatureValue(FeatureValues,smileys,word);
			if(smileys!=14)
			{
				cout<<"Problem Houston"<<endl;
				system("pause");
			}
			//cout<<"Number of commas is "<<smileys<<endl;
			theTable.push_back(row);
		}//if (strLine != "")
    }//while (getline(input,strLine))

	cout<<endl<<endl<<"Now printing the feature values"<<endl;
	printFeatureValues(Features, FeatureValues);
	

	//cout<<endl<<endl<<"Now printing the table"<<endl;
	//printTheTable(theTable);
	
	
		
	cout<<"NOW FINDING THE CASUAL RULES"<<endl;
	int input1CTRL = 0, input2CTRL = 0, outputCTRL = 0;
	//system("pause");
	for(int input1_i = 0; input1_i<15; input1_i++)
	{
		for(int input1_j = 0; input1_j<15; input1_j++)
		{
			if(FeatureValues[input1_i][input1_j]=="CTRL")
			{
				input1CTRL++;
				if(input1CTRL>1)
					continue;
			}
			for(int input2_i = input1_i+1; input2_i<15; input2_i++)
			{				
				for(int input2_j = 0; input2_j<15; input2_j++)
				{
					if(FeatureValues[input2_i][input2_j]=="CTRL")
					{
						input2CTRL++;
						if(input2CTRL>1)
							continue;
					}
					for(int output_i = 0; output_i<15; output_i++)
					{
						if((output_i == input1_i)||(output_i == input2_i))
							continue;
						for(int output_j = 0; output_j<15; output_j++)
						{
							if(FeatureValues[output_i][output_j]=="CTRL")
							{
								outputCTRL++;
								if(outputCTRL>1)
									continue;
							}
							int inputsMatchOnly=0, outputsAndInputsMatch = 0;
							for(int table_i = 0; table_i<theTable.size(); table_i++)
							{
								if((theTable[table_i][input1_i]==FeatureValues[input1_i][input1_j])&&
								   (theTable[table_i][input2_i]==FeatureValues[input2_i][input2_j]))
								{
									inputsMatchOnly++;
									/*cout<<"------------------------------------"<<endl;
									cout<<"theTable["<<table_i<<"]["<<input1_i<<"]="<<theTable[table_i][input1_i]<<endl;
									cout<<"FeatureValues["<<input1_i<<"]["<<input1_j<<"]="<<FeatureValues[input1_i][input1_j]<<endl<<endl;

									cout<<"theTable["<<table_i<<"]["<<input2_i<<"]="<<theTable[table_i][input2_i]<<endl;
									cout<<"FeatureValues["<<input2_i<<"]["<<input2_j<<"]="<<FeatureValues[input2_i][input2_j]<<endl<<endl;
									cout<<"------------------------------------"<<endl;*/
									if(theTable[table_i][output_i]==FeatureValues[output_i][output_j])
									{
										outputsAndInputsMatch++;
									}
								}								
							}//for(int table_i = 0; table_i<theTable.size(); table_i++)
							//cout<<"------------------------------------"<<endl;
							//cout<<"inputsMatchOnly="<<inputsMatchOnly<<endl;
							//cout<<"outputsAndInputsMatchy="<<outputsAndInputsMatch<<endl<<endl;
							long double PX = (long double) inputsMatchOnly/theTable.size();
							long double PXY = (long double) outputsAndInputsMatch/theTable.size();
							long double HYX = PXY*(log(PXY)/log(PX)); 
							if((HYX<0.08) && (outputsAndInputsMatch>9))
							{
								cout<<"------------------------------------"<<endl;
								cout<<"HYX="<<HYX<<endl;
								cout<<"inputsMatchOnly="<<inputsMatchOnly<<endl;
								cout<<"outputsAndInputsMatchy="<<outputsAndInputsMatch<<endl<<endl;
								cout<<"Feature 1="<<Features[input1_i]
								<<", value="<<FeatureValues[input1_i][input1_j]<<endl;

								cout<<"Feature 2="<<Features[input2_i]
								<<", value="<<FeatureValues[input2_i][input2_j]<<endl;

								cout<<"=>"<<endl;
								cout<<"Feature="<<Features[output_i]
								<<", value="<<FeatureValues[output_i][output_j]<<endl<<endl;

								output<<"------------------------------------"<<endl;
								output<<"HYX="<<HYX<<endl;
								output<<"inputsMatchOnly="<<inputsMatchOnly<<endl;
								output<<"outputsAndInputsMatchy="<<outputsAndInputsMatch<<endl<<endl;
								output<<"Feature 1="<<Features[input1_i]
								<<", value="<<FeatureValues[input1_i][input1_j]<<endl;

								output<<"Feature 2="<<Features[input2_i]
								<<", value="<<FeatureValues[input2_i][input2_j]<<endl;

								output<<"=>"<<endl;
								output<<"Feature="<<Features[output_i]
								<<", value="<<FeatureValues[output_i][output_j]<<endl<<endl;
							}
							
						}
					}
				}
			}
		}
	}

}

int main()
{
	ifstream input;
	ofstream output;
	string strLine;

	string inFileName = "shkurte.csv";
	string outFileName = "casual rules.txt";

	input.open(inFileName.c_str());
	if (input.fail())
	{
		cout << "Error: Cannot open file "<< inFileName << endl ;
	}
	else
	{
		output.open(outFileName.c_str());
		if (output.fail())
		{
			cout << "Error: Cannot open file " << outFileName << endl ;
		}
		else
		{
			processFile(input,output);
		}
		output.close();
	}
	system("pause");
	return 0;
}

