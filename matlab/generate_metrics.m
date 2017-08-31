function results_listing = generate_metrics(dir_list)
    
    % Add PICMUS path
    addpath(genpath('picmus'));
    
    % Load the scan object
    url = 'https://www.creatis.insa-lyon.fr/EvaluationPlatform/picmus/dataset/';
    picmus_scan_path = '../data/picmus17/';
    scan_filename = 'scanning_region_picmus.hdf5';
    
    %-- create the scan object
    scan = linear_scan();
    scan.read_file(fullfile(picmus_scan_path, scan_filename));
    for ll = 1:numel(dir_list)
        dir_name = dir_list{ll};
        % Get a listing of all the .mat files in dir_name
        results_listing=dir(fullfile(dir_name,'*.mat'));
        C = strsplit(dir_name, '/');
        solver_type = strjoin(C(end));

        for kk = 1:size(results_listing,1)
            cur_list = results_listing(kk,:);
            
            if not(contains(cur_list.name, 'metrics'))
                % Load the filename from the current list
                file_name = fullfile(cur_list.folder, cur_list.name);
                load(file_name);

                disp(['************ ', cur_list.name, ' ************'])
                % Take the envelope of the RF image and interpolate on the scan
                envelope = tools.envelope(rf_data);
                [Xim, Zim] = meshgrid(xim ,zim);
                reshaped_envelope =interp2(Xim, Zim , envelope, scan.x_matrix, scan.z_matrix, 'linear', 0);

                % Store the envelope in image object
                image = us_image(solver_type);
                image.author = 'Adrien Besson <adrien.besson.epfl@ch>';
                image.affiliation = 'Adrien Besson';
                image.algorithm = solver_type;
                image.scan = scan;
                image.number_plane_waves = number_plane_waves;
                image.data = reshaped_envelope;
                image.transmit_f_number = 0;
                image.receive_f_number = 0;
                image.transmit_apodization_window = 'none';
                image.receive_apodization_window = 'none';

                % Generate the info structure to store the results
                pht_type = get_pht_type(cur_list.name);
                if ischar(pht_type)
                    info = tools.generate_data_info_structure(pht_type);

                    % Create picmus metric data object
                    metrics = us_picmus_metrics();
                    metrics.image = image;
                    metrics.scan = image.scan;
                    metrics.set_data_information(info);
                    metrics.flagDisplay = 0; % Set this flag to 1 to display intermediate results
                    
                    % Evaluate resolution and contrast
                    metrics.evaluateFWHM();
                    metrics.evaluateContrast();
                    
                    %-- Select the right quality indicator in the metric object
                    resolution = squeeze(metrics.scoreFWHM);
                    contrast = metrics.scoreContrast;
                    
                    %-- Export metrics of interest
                    format = '.mat';
                    C = strsplit(file_name, format);
                    output_filename = strcat([strjoin(C(1)), '_metrics', format]);
                    save(output_filename, 'resolution', 'contrast');
                else
                    disp('No metric computation possible')
                end
            end
        end
    end
    
end
