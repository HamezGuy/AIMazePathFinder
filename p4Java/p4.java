import java.io.File;
import java.io.FileNotFoundException;
import java.security.Key;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;
import java.util.Set;

public class p4 {

	private static final int K = 8;               // number of clusters to generate
	private static final int FEATURE_LENGTH = 3;  // number of parameters used in the algorithms

	public static void main(String[] args) {

		/*
		 * Latitude, longitude and total number of deaths are used as parameters.
		 *  - for latitude and longitude average value is taken if country appears more than once;
		 *  - for total number of deaths sum of the last column is used if country appears more than once.
		 */
		/*
		 * TODO: For your submission you need to implement Part 1 for finding suitable parameters. 
		 */
		Map<String, Double[]> globalData = preprocessData("allDeaths.csv");

		

		Set<String> countries = globalData.keySet();
		List<String> sortedListCountries = new ArrayList<>(countries);
		Collections.sort(sortedListCountries);
		
		List<Double[]> global_data = new ArrayList<Double[]>();
		for (String country: sortedListCountries){
			global_data.add(globalData.get(country));
		}


		Map<String, Double[]> makeParameterMatrix = makeParameterMatrix(globalData);
		

		// Hierarchical Clustering with single-linkage and Manhattan distance
		List<List<String>> clusters = new ArrayList<List<String>>();

		// each country appears as a separate cluster at the beginning
		for (int i=0; i<sortedListCountries.size(); i++){
			List<String> cluster = new ArrayList<String>();
			cluster.add(sortedListCountries.get(i));
			clusters.add(cluster);
		}

		

		while (clusters.size() != K ){

			double minimumDistance = Double.MAX_VALUE;
			List<String> clusterToMerge1 = null, clusterToMerge2 = null;
			int indexCluster1 = -1, indexCluster2 = -1;

			for (int i=0; i<clusters.size(); i++){
				List<String> cluster1 = clusters.get(i);
				for (int j=i+1; j<clusters.size(); j++){ // make sure it's not the same cluster though, otherwise dist is 0.

					List<String> cluster2 = clusters.get(j);
					// compute single linkage distance between given two clusters
					
					double currDist = singleLinkageDistance(globalData, cluster1, cluster2); 

					if (currDist < minimumDistance) {
						minimumDistance = currDist;
						clusterToMerge1 = cluster1;
						clusterToMerge2 = cluster2; 
						indexCluster1 = i;
						indexCluster2 = j;
					}
				}
			}

			// need to merge those two clusters with min distance
			if (clusterToMerge1!=null && clusterToMerge2!=null){

				clusters.remove(indexCluster2);
				clusters.remove(indexCluster1);

				clusterToMerge1.addAll(clusterToMerge2);
				clusters.add(clusterToMerge1);
			} else{
				System.out.println("Something is incorrect, one cluster might be null.");
				System.exit(1);
			}
		}

		// Print out final clusters
		System.out.println("Hierarchical Clustering Results: ");
		int cluster_num = 0;
		HashMap<String, Integer> clusterHier = new HashMap<String, Integer>();
		for (List<String> l : clusters){
			System.out.println(cluster_num + " " + l);

			for (int i=0; i<l.size(); i++){
				String country = l.get(i);
				clusterHier.put(country, cluster_num);
			}
			cluster_num++;
		}
		System.out.println("=============================================================");

		int[] cluster_info = new int[sortedListCountries.size()]; // cluster to which country is assigned to

		// K-Means Clustering with Manhattan distance

		// K vectors of length FEATURE_LENGTH, those will hold our cluster centers
		List<Double[]> means = new ArrayList<Double[]>(); 
		// Choose K random countries as our initial means for cluster centers
		for (int i=0; i < K; i++){
			Random r = new Random();
			int rand = r.nextInt(sortedListCountries.size());
			Double[] vector = global_data.get(rand); 
			means.add(vector);
		}

		// find initial cluster assignment for all countries
		findClusterForCountries(global_data, means, cluster_info);

		// start updating means for clusters until clusters do not change
		boolean keepUpdatingMeans = true;

		List<Double[]> previous_iteration_means = means;

		while (keepUpdatingMeans){

			List<Double[]> recomputed_means = recomputeMeans(global_data, cluster_info);

			// need to make sure that all K means are not changing for stopping learning algorithm
			int checker = 0;
			for(int cl_index=0; cl_index<K; cl_index++){

				if (Arrays.equals(recomputed_means.get(cl_index), previous_iteration_means.get(cl_index))){
					checker+=1;
				}
			}
			if (checker == K){
				// all K vectors are still the same after last iteration of updates to the means
				// therefore stop the algorithm
				keepUpdatingMeans = false;
				break;
			}
			findClusterForCountries(global_data, recomputed_means, cluster_info);
			previous_iteration_means = recomputed_means;
		}

		// Print out list of countries in each cluster for K-Means
		System.out.println("K-Means Clustering Results: ");
		for (int i=1; i<K+1; i++){
			System.out.print(i-1 + " [");
			StringBuilder sb = new StringBuilder();
			for (int j=0; j<sortedListCountries.size(); j++){
				if (cluster_info[j] == i){
					sb.append(sortedListCountries.get(j) + ", ");
				}
			}
			if (sb.length() != 0)System.out.print(sb.toString().substring(0,sb.length()-2));
			else System.out.print(sb.toString());
			System.out.print("]");
			System.out.println();
		}

	}
	

	public static Map<String, Double[]> makeParameterMatrix(Map<String, Double[]> globalData)
	{
		Map<String, Double[]> meanList = meanValues(globalData);
		Map<String, Double[]> normalList = normalDistribution(globalData);
		Map<String, Double[]> doubleInfection = daysToDoubleInfection(globalData);
		Map<String, Double[]> linearRegression = linearRegression(globalData);
		Map<String, Double[]> percentInfected = percentInfected(globalData);
		
		Map<String, Double[]> allArray = new HashMap<String, Double[]>();

		

		for(int i = 0; i < meanList.size(); i ++)
		{
			String key = meanList.getKey();
			if(allArray.containsKey(key))
			{
				allArray.get(key).add(value);

			}
			else{
				System.out.println("Error could not find key");
			}
			allArray[i][0] = meanList.get(i);
			allArray[i][1] = normalList.get(i);
			allArray[i][2] = doubleInfection.get(i);
			allArray[i][3] = linearRegression.get(i);
			allArray[i][4] = percentInfected.get(i);
		}
		

		return allArray;
	}

	private static Map<String, Double[]> meanValues(Map<String, Double[]> globalData)
	{
		List<Double> returnValue = new ArrayList<Double>();

		for(Double[] array : globalData)
			{
				double allNumsInt = 0;
				double overallNums= 0;

				for(Double x : array)
				{
					overallNums += x;
					allNumsInt ++;
				}

				double mean = overallNums/allNumsInt;
				returnValue.add(mean);
			}

		return returnValue;
	}
	private static Map<String, Double[]> normalDistribution(Map<String, Double[]> globalData)
	{
		List<Double> returnValue = new ArrayList<Double>();
		for(Double[] array : globalData)
			{
				double allNumsInt = 0;
				double overallNums= 0;

				for(Double x : array)
				{
					overallNums += x;
					allNumsInt ++;
				}

				double mean = overallNums/allNumsInt;
				returnValue.add(mean);
			}
		return returnValue;
	}
	private static Map<String, Double[]> daysToDoubleInfection(Map<String, Double[]> globalData)
	{
		List<Double> returnValue = new ArrayList<Double>();
		for(Double[] array : globalData)
			{
				double allNumsInt = 0;
				double overallNums= 4;

				for(Double x : array)
				{
					overallNums += x;
					allNumsInt ++;
				}

				double mean = overallNums/allNumsInt;
				returnValue.add(mean);
			}
		return returnValue;
	}
	private static Map<String, Double[]> linearRegression(Map<String, Double[]> globalData)
	{
		List<Double> returnValue = new ArrayList<Double>();
		for(Double[] array : globalData)
			{
				double allNumsInt = 0;
				double overallNums= 8;

				for(Double x : array)
				{
					overallNums += x;
					allNumsInt ++;
				}

				double mean = overallNums/allNumsInt;
				returnValue.add(mean);
			}
		return returnValue;
	}
	private static Map<String, Double[]> percentInfected(Map<String, Double[]> globalData)
	{
		List<Double> returnValue = new ArrayList<Double>();
		for(Double[] array : globalData)
			{
				double allNumsInt = 0;
				double overallNums= 16;

				for(Double x : array)
				{
					overallNums += x;
					allNumsInt ++;
				}

				double mean = overallNums/allNumsInt;
				returnValue.add(mean);
			}
		return returnValue;
	}
	

	/*
	 * Before using the input csv file, I deleted commas for two cells: 
	 * "Korea South" and "Bonaire Sint Eustatius and Saba". 
	 * You might need to do that as well if you decide to use this code for
	 * preprocessing. 
	 */
	public static Map<String, Double[]> preprocessData(String file) {

		Map<String, Integer> numOfOccurrences = new HashMap<String,Integer>();
		Map<String,Double[]> globalData = new HashMap<String, Double[]>();

		try {
			Scanner sc = new Scanner(new File(file));
			String firstLineColumnNames = sc.nextLine();

			

			int totalNumColumns = firstLineColumnNames.split(",").length;

			while (sc.hasNext()){
				String[] line = sc.nextLine().split(",");

				Double[] countryInfo = new Double[totalNumColumns - 14];
				
				for(int i = 14; i < totalNumColumns; i++)
				{
					int x = i - 14;
					countryInfo[x] = Double.valueOf(line[i]);
				}
				
				

				if (globalData.containsKey(line[6])){
					
					// get previous values
					Double[] prevData = globalData.get(line[6]); 

					// sum values for the same state
					for (int j=0; j<prevData.length; j++){
						countryInfo[j] = countryInfo[j] + prevData[j];
					}
					numOfOccurrences.put(line[1], numOfOccurrences.get(line[6]) + 1); // increase counter
					globalData.put(line[1], countryInfo);


				} else {

					globalData.put(line[6], countryInfo);
					numOfOccurrences.put(line[6], 1);
				}
			}

			// find average for latitude and longitude for countries that have several occurrences
			for (String country: numOfOccurrences.keySet()){

				int count = numOfOccurrences.get(country);
				System.out.println("Country, number of occurances " + numOfOccurrences.get(country));
				if (count > 1){
					Double[] list = globalData.get(country);

					// index 0 - latitude
					// index 1 - longitude

					for(int i = 0; i < list.length; i ++)
					{
						list[i] = (double) list[i]/count;
					}

					globalData.put(country, list);
				}
			}
			sc.close();
		} catch (FileNotFoundException e) {
			System.out.println("The input file cannot be found! ");
		}

		if (globalData.containsKey("Wisconsin"))
		{
			Double[] wiscData = globalData.get("Wisconsin");
			for(int i = 0; i < wiscData.length; i++ )
			{
				if(i != ( wiscData.length - 1) )
				{
					System.out.print(wiscData[i] + ",");
				}
				else{
					System.out.print(wiscData[i]);
				}
			}
 
			System.out.println();
		}

		if(globalData.containsKey("Alabama"))
		{
			Double[] alabData = globalData.get("Alabama");
			for(int i = 0; i < alabData.length; i++ )
			{
				if(i != ( alabData.length - 1) )
				{
					System.out.print(alabData[i] + ",");
				}
				else{
					System.out.print(alabData[i]);
				}
			}

			System.out.println();
		}


		
		double consecNumberAlab = 0;
		double changeInNumberAlab = 0;
		if(globalData.containsKey("Wisconsin"))
		{
			System.out.println();
			Double[] wiscData = globalData.get("Wisconsin");
			double consecNumberWisc = 0;
			double changeInNumberWisc = 0;
			
			for(int i = 0; i < wiscData.length ; i++ )
			{
				
				if(i == 0)
				{
					continue;
				}

				if(wiscData[i].equals(wiscData[(i-1)]))
				{
					consecNumberWisc = wiscData[i];
				}
				else{
					changeInNumberWisc = ( wiscData[i] - consecNumberWisc );
					
				}
				

				
				if(i != ( wiscData.length - 1) )
				{
					System.out.print(changeInNumberWisc + ",");
				}
				else{
					System.out.print(changeInNumberWisc);
				}
			}
			System.out.println();
		}

		if(globalData.containsKey("Alabama"))
		{
			System.out.println();
			Double[] wiscData = globalData.get("Alabama");

			for(int i = 0; i < wiscData.length ; i++ )
			{
				
				if(i == 0)
				{
					continue;
				}

				if(wiscData[i].equals(wiscData[i-1]))
				{
					consecNumberAlab = wiscData[i];
					
				}
				else{
					changeInNumberAlab = wiscData[i] - consecNumberAlab;
				}
				
				if(i != ( wiscData.length - 1) )
				{
					System.out.print(changeInNumberAlab + ",");
				}
				else{
					System.out.print(changeInNumberAlab);
				}
			}
			System.out.println();
		}




		return globalData;
	}

	/*
	 * This method computes single-linkage distance between two clusters. 
	 * Makes use of Manhattan distance. 
	 */
	public static double singleLinkageDistance( Map<String, Double[]> globalData, List<String> cluster1, List<String> cluster2){

		double minDistance = Double.MAX_VALUE;
		double distance; 
		for (int i=0; i<cluster1.size(); i++){
			for (int j=0; j<cluster2.size(); j++){

				distance = 0;

				Double[] values1 = globalData.get(cluster1.get(i));
				Double[] values2 = globalData.get(cluster2.get(j));

				for (int m=0; m<values1.length; m++){
					// TODO: change this part of code to use Euclidean distance
					distance += Math.pow((values1[m] - values2[m]), 2);
				}
				if (distance < minDistance) minDistance = distance;
			}
		}
		return minDistance;
	}

	/*
	 * This method given input on parameters for each country, and information about 
	 * means for the clusters, assigns each country to the cluster and updates the 
	 * array holding information about the assignment. 
	 */
	private static void findClusterForCountries(List<Double[]> data, List<Double[]> means, int[] cluster_info) {

		for (int i=0; i<data.size(); i++){
			Double[] countryInfo = data.get(i);

			int min_cluster = 0;
			double min_distance = Double.MAX_VALUE;

			for (int k = 0; k<K; k++){

				Double[] mean_vector = means.get(k);
				double distance = 0;

				// Manhattan distance 
				for (int j=0; j < countryInfo.length; j++){
					// TODO: change this to Euclidean distance instead of Manhattan
					distance += Math.pow(countryInfo[j] - mean_vector[j], 2); 
				}

				if (distance<min_distance){
					min_cluster = k+1;
					min_distance = distance;
				}
			}
			cluster_info[i] = min_cluster;
		}
	}
	
	/*
	 * This method given all countries' information and a new assignment of countries to the clusters, 
	 * recomputes the means for clusters by finding the average.
	 */
	private static List<Double[]> recomputeMeans(List<Double[]> countries, int[] cluster_info){
		
		List<Double[]> means = new ArrayList<Double[]>();
		
		// consider each cluster
		for (int i=0; i < K; i++){

			int cluster_size = 0;
			Double[] cluster_mean = new Double[FEATURE_LENGTH];
			
			// initialize values to 0, to avoid null pointer
			for (int k=0;k<cluster_mean.length; k++){
				cluster_mean[k] = 0.0;
			}

			for (int j=0; j< cluster_info.length; j++){

				if (cluster_info[j] == i+1){

					cluster_size += 1;

					Double[] countryInfo = countries.get(j);

					// sum values for all countries in the cluster
					for (int index = 0; index<countryInfo.length; index++){
						cluster_mean[index] += countryInfo[index];
					}
				}
			}

			// average all countries in the cluster 
			for (int index = 0; index<cluster_mean.length; index++){
				cluster_mean[index] = cluster_mean[index]/(double)cluster_size;
			}
			means.add(cluster_mean);
		}
		return means;
	}
}